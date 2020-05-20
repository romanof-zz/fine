//
//  Portfolio.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit
import DynamicCodable

struct StockItem: Decodable {
    var symbol: String = ""
    var percent: Double = 0
    var close: Double = 0
    var open: Double = 0
}

struct PortfolioValue: Decodable {
    var open: Double
    var close: Double
}

class Portfolio: Decodable {
    var value: PortfolioValue
    var timeSeries: [String : [String: Any]] = [:]

    var stocks: [StockItem] = []

    private enum CodingKeys: String, CodingKey {
        case value, timeSeries = "time_series", stocks
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        let timeSeriesDic = try container.decode([String: Any].self, forKey: .timeSeries)

        if let timeSeriesDic = timeSeriesDic as? [String: [String: Any]] {
            timeSeries = timeSeriesDic
        }
        
        stocks = try container.decode([StockItem].self, forKey: .stocks).sorted(by: { (item1, item2) -> Bool in
            return item1.percent > item2.percent
        })

        value = try container.decode(PortfolioValue.self, forKey: .value)
    }
}
