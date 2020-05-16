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

        return true
    }
}

