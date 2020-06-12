package com.fine;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class FragYoutubePlay extends Fragment {
    WebView webView;
    String url;

    public FragYoutubePlay() {}

    public FragYoutubePlay(String url) {
        this.url = url;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        if (getArguments() != null) {
            this.url = getArguments().getString("url");
        }
        View root = inflater.inflate(R.layout.frag_youtube_play, container, false);
        webView = root.findViewById(R.id.frag_youtube_play_webView);

        // Enable Javascript
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);

        // Force links and redirects to open in the WebView instead of in a browser
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl(url);
        return root;
    }

}
