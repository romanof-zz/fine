//
//  Portfolio.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit
import DynamicCodable

struct StockItem {
    var name: String = ""
    var percent: Double = 0
    var close: Double = 0
    var open: Double = 0
}

class Portfolio: Decodable {
    var value: Float
    var timeSeries: [String : [String: Any]] = [:]

    var stocks: [StockItem] = []

    private enum CodingKeys: String, CodingKey {
        case value, timeSeries = "time_series", stocks
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        value = try container.decode(Float.self, forKey: .value)

        let timeSeriesDic = try container.decode([String: Any].self, forKey: .timeSeries)

        if let timeSeriesDic = timeSeriesDic as? [String: [String: Any]] {
            timeSeries = timeSeriesDic

            //refactor this crap
            if let stocksValues = timeSeriesDic["stocks"] as? [String: [String: Any]] {
                for (key, value) in stocksValues {
                    let percent = value["percent"] as? Double ?? (Double(value["percent"] as? Int ?? 0))
                    let close = value["close"] as? Double ?? 0
                    let open = value["open"] as? Double ?? 0
                    let stockItem = StockItem(name: key, percent: percent, close: close, open: open)
                    stocks.append(stockItem)
                }
            }
            stocks.sort(by: { $0.name < $1.name })
        }

    }
}
