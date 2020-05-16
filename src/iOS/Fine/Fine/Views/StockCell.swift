//
//  StockCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit

class StockCell: BaseTableViewCell {

    @IBOutlet weak var priceBkgView: UIView!
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var companyLabel: UILabel!

    func setup(with stockItem: StockItem) {
        companyLabel.text = "\(stockItem.name) (\(stockItem.percent))" -> move to right, closer to the price

        (close - open) /close on tap

        baraban

        0.1 - 100, default 1, step 0.1

        smooth graph

        Fine logo

        priceLabel.text = String(format: "$%.02f", stockItem.close)

        if stockItem.open > stockItem.close {
            priceBkgView.backgroundColor = UIColor(red: 255/255, green: 45/255, blue: 85/255, alpha: 1)
            priceLabel.textColor = UIColor(hex: "5E0025")
        } else {
            priceBkgView.backgroundColor = .green
            priceLabel.textColor = UIColor(hex: "075125")
        }
    }
}
