//
//  Portfolio.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit
import DynamicCodable

class Portfolio: Decodable {
    var value: Float
    var timeSeries: [String : [String: Any]] = [:]

    var stocks: [String: [String: Any]]  {
        if let stocksValue = timeSeries["stocks"] as? [String: [String: Any]] {
            return stocksValue
        } else {
            return [:]
        }
    }

    private enum CodingKeys: String, CodingKey {
        case value, timeSeries = "time_series", stocks
    }

    required init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        value = try container.decode(Float.self, forKey: .value)

        let timeSeriesDic = try container.decode([String: Any].self, forKey: .timeSeries)

        if let timeSeriesDic = timeSeriesDic as? [String: [String: Any]] {
            timeSeries = timeSeriesDic
        }

    }
}
