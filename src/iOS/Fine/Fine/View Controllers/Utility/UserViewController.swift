//
//  UserViewController.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 20/05/2020.
//

import UIKit

class UserViewController: UIViewController {

    @IBOutlet weak var label: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        label.text = DataManager.shared.user?.name

        if let urlString = DataManager.shared.user?.imageUrl,
            let url = URL(string: urlString) {
            imageView.af_setImage(withURL: url)
        }
    }
}
