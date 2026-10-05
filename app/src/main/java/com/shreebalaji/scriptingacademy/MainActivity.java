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
        @JavascriptInterface
        public String runtime() {
            return "{\"platform\":\"Android\",\"engine\":\"Android WebView\",\"realJavaScript\":true,\"nativeToolchain\":\"NDK build-time only\",\"windowsExecution\":false}";
        }

        @JavascriptInterface
        public String version() {
            return "REAL-LAB-V12";
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
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return loader.shouldInterceptRequest(request.getUrl());
            }

            @Override public WebResourceResponse shouldInterceptRequest(WebView view, String url) {
                return loader.shouldInterceptRequest(android.net.Uri.parse(url));
            }

            @Override public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
            }

            @Override public boolean onRenderProcessGone(WebView view, android.webkit.RenderProcessGoneDetail detail) {
                Toast.makeText(MainActivity.this, "Learning engine restarted.", Toast.LENGTH_SHORT).show();
                return true;
            }
        });

        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setSupportMultipleWindows(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);

        webView.addJavascriptInterface(new AcademyBridge(), "AcademyNative");
        webView.loadUrl("https://appassets.androidplatform.net/assets/index.html");
        setContentView(webView);
    }

    private void injectRealLab() {
        String js =
            "(function(){"
          + "if(window.__realLabV8)return;window.__realLabV8=1;"
          + "var lab=document.getElementById('labcenter');if(!lab)return;"
          + "var box=document.createElement('div');box.className='card v7hero';box.id='realLabV8';"
          + "box.innerHTML='<h2>⚡ REAL LAB V9</h2>'"
          + "+'<p><b>No fake success messages.</b> The Academy now labels exactly what is really executed.</p>'"
          + "+'<div id="rlStatus" class="teacherBox">Checking runtime…</div>'"
          + "+'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">'"
          + "+'<button class="btn primary" id="rlSelf">Android Runtime Self-Test</button>'"
          + "+'<button class="btn" id="rlWin">Connect Windows Lab Agent</button>'"
          + "+'</div>'"
          + "+'<div id="rlWinBox" style="display:none;margin-top:12px">'"
          + "+'<input id="rlUrl" class="search" value="http://127.0.0.1:8765" placeholder="Windows Lab Agent URL">'"
          + "+'<button class="btn" id="rlHealth">Test Connection</button><pre id="rlOut" class="terminal">Not connected.</pre></div>';"
          + "lab.insertBefore(box,lab.firstChild);"
          + "var s=document.getElementById('rlStatus');"
          + "try{var r=JSON.parse(AcademyNative.runtime());s.innerHTML='🟢 <b>REAL:</b> JavaScript runs inside the Android WebView. '+r.nativeToolchain+'. Windows execution is not claimed.';}catch(e){s.textContent='🟡 Browser mode: native runtime bridge unavailable.';}"
          + "document.getElementById('rlSelf').onclick=function(){"
          + "var a=7,b=5,result=a*b+2;"
          + "document.getElementById('rlOut').textContent='REAL Android WebView JavaScript\\n7 * 5 + 2 = '+result+'\\nEngine: '+(navigator.userAgent||'WebView');};"
          + "document.getElementById('rlWin').onclick=function(){var x=document.getElementById('rlWinBox');x.style.display=x.style.display==='none'?'block':'none';};"
          + "document.getElementById('rlHealth').onclick=async function(){"
          + "var url=(document.getElementById('rlUrl').value||'').replace(/\\/$/,'');var out=document.getElementById('rlOut');"
          + "out.textContent='Connecting…';try{var res=await fetch(url+'/health');var txt=await res.text();out.textContent=res.ok?'🟢 WINDOWS LAB AGENT ONLINE\\n'+txt:'🔴 Agent returned HTTP '+res.status+'\\n'+txt;}catch(e){out.textContent='🔴 Not connected. Start tools/windows-lab-agent.py on the Windows PC and use the displayed localhost URL.';}"
          + "};"
          + "})();";
        webView.evaluateJavascript(js, null);
    }

    @Override public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    @Override protected void onDestroy() {
        if (webView != null) {
            webView.removeJavascriptInterface("AcademyNative");
            webView.stopLoading();
            webView.clearHistory();
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
