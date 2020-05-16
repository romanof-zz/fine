//
//  AppDelegate.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {

        UINavigationBar.appearance().tintColor = .main

        refreshPortfolio()

        return true
    }

    @objc private func refreshPortfolio() {
        DataManager.shared.networkManager.fetchPortfolio {[weak self] (response) in
            //self?.refreshControl.endRefreshing()

            switch response {
            case .Success(let portfolio):
                //                self?.posts = posts
                //                self?.tableView.reloadData()
                print(portfolio.stocks)
            case .Error(_):
                Utils.showAlert(with: "Error fetching portfolio")
            }
        }
    }

}

