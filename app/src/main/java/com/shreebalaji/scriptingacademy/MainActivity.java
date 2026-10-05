package com.shreebalaji.scriptingacademy;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewClientCompat;

public class MainActivity extends Activity {
    private WebView webView;
    public final class AcademyBridge {
        @JavascriptInterface public String runtime() {
            return "{\"platform\":\"Android\",\"engine\":\"Android WebView\",\"realJavaScript\":true,\"windowsExecution\":\"Windows Lab Agent\",\"fakeExecution\":false}";
        }
        @JavascriptInterface public String version() { return "REAL-LAB-V20"; }
        @JavascriptInterface public String capabilities() {
            return "{\"apk\":true,\"webview\":true,\"javascript\":true,\"localStorage\":true,\"windowsAgent\":true,\"truthfulExecution\":true}";
        }
    }
    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        webView = new WebView(this);
        webView.setBackgroundColor(0xFF090B14);
        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
            .addPathHandler("/res/", new WebViewAssetLoader.ResourcesPathHandler(this))
            .build();
        webView.setWebViewClient(new WebViewClientCompat() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest r) { return loader.shouldInterceptRequest(r.getUrl()); }
            @Override public WebResourceResponse shouldInterceptRequest(WebView v, String url) { return loader.shouldInterceptRequest(android.net.Uri.parse(url)); }
            @Override public boolean onRenderProcessGone(WebView v, android.webkit.RenderProcessGoneDetail d) {
                Toast.makeText(MainActivity.this,"Learning engine restarted.",Toast.LENGTH_SHORT).show(); return true;
            }
        });
        WebSettings s=webView.getSettings();
        s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false); s.setAllowContentAccess(false);
        s.setSupportMultipleWindows(false); s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false); s.setMediaPlaybackRequiresUserGesture(true);
        webView.addJavascriptInterface(new AcademyBridge(),"AcademyNative");
        webView.loadUrl("https://appassets.androidplatform.net/assets/index.html");
        setContentView(webView);
    }
    @Override public void onBackPressed() { if(webView!=null&&webView.canGoBack()) webView.goBack(); else super.onBackPressed(); }
    @Override protected void onDestroy() {
        if(webView!=null){webView.removeJavascriptInterface("AcademyNative");webView.stopLoading();webView.clearHistory();webView.destroy();webView=null;}
        super.onDestroy();
    }
}
