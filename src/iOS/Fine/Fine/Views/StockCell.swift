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
        companyLabel.text = stockItem.name

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
