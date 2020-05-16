//
//  BaseViewController.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit

class BaseViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

       setupNavbar()
    }

    private func setupNavbar() {
        //        title = "Fine 🔥"
        //        let titleDict: NSDictionary = [NSAttributedString.Key.foregroundColor: UIColor.white]
        //        navigationController?.navigationBar.titleTextAttributes = titleDict as? [NSAttributedString.Key : Any]


        let imageView = UIImageView(image: UIImage(named: "nav_logo"))
        imageView.contentMode = .scaleAspectFit
        self.navigationItem.titleView = imageView

        self.navigationController?.navigationBar.setBackgroundImage(UIImage(), for: UIBarMetrics.default)
        self.navigationController?.navigationBar.shadowImage = UIImage()

        navigationController?.navigationBar.barTintColor = .main
        navigationController?.navigationBar.isTranslucent = false
    }

}
