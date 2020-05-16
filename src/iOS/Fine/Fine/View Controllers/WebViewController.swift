//
//  WebViewController.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit
import WebKit

class WebViewController: UIViewController {
    var urlString: String?

    @IBOutlet weak var webView: WKWebView!
    override func viewDidLoad() {
        super.viewDidLoad()

        guard let urlString = urlString,
            let url = URL(string: urlString) else { return }

        let request = URLRequest(url: url)
        webView.load(request)

    }
}
