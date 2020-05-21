//
//  VideoPostCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit
import AlamofireImage

class VideoPostCell: BasePostCell {

    @IBOutlet weak var previewImageView: UIImageView!
    var urlString: String?

    @IBOutlet weak var playButton: UIButton!

    override func setup(with post: Post) {
        guard let urlString = post.details.url,
            let url = URL(string: urlString) else { return }

        self.urlString = post.details.url

        if let videoId = url.queryParameters?["v"] {
            let imageUrl = "https://img.youtube.com/vi/\(videoId)/0.jpg"
            if let imageUrl = URL(string: imageUrl) {
                previewImageView.af_setImage(withURL: imageUrl)
            }
        }
    }

    @IBAction func buttonTapped(_ sender: Any) {
        let webVC: WebViewController = Utils.instantiateVC(from: "Main")
        webVC.urlString = urlString

        guard let tabbar = UIApplication.shared.keyWindow?.rootViewController as? UITabBarController, let navbar = tabbar.selectedViewController as? UINavigationController else { return }

        navbar.pushViewController(webVC, animated: true)
    }
}
