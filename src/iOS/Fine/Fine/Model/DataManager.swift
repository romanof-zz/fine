//
//  DataManager.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 14/05/2020.

//

import UIKit

private let baseUrl = "https://finedata.org"

class DataManager: NSObject {
    static let shared = DataManager()

    let networkManager = NetworkManager(baseUrl: baseUrl, api: "")
//    let stateManager = StateManager()
//    let purchaseManager = PurchaseManager()

    var user: User?

    let userColors: [Int: String] = [0: "000000", 1 : "4287f5", 2: "a63ae0", 3: "24ab1d"]
}
