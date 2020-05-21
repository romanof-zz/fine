//
//  StockCell.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import UIKit

class StockCell: BaseTableViewCell {

    @IBOutlet weak var percentLabel: UILabel!
    @IBOutlet weak var priceBkgView: UIView!
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var companyLabel: UILabel!

    private var stockItem: StockItem?

    private var toggled = false

    var percentMode = false

    override func prepareForReuse() {
        super.prepareForReuse()
        contentView.backgroundColor = .clear
    }
    
    func setup(with stockItem: StockItem, percentMode: Bool) {
        self.stockItem = stockItem
        self.percentMode = percentMode
        redraw()
    }

    private func redraw() {
        guard let stockItem = stockItem else { return }

        companyLabel.text = stockItem.symbol

        percentLabel.text = "\(stockItem.percent)%"

        let value = percentMode ? (stockItem.close - stockItem.open) / stockItem.close : stockItem.close
        priceLabel.text = String(format: percentMode ? "%.02f %%" : "$%.02f", value)

        if stockItem.open > stockItem.close {
            priceBkgView.backgroundColor = UIColor(red: 255/255, green: 45/255, blue: 85/255, alpha: 1)
            priceLabel.textColor = UIColor(hex: "5E0025")
        } else {
            priceBkgView.backgroundColor = .green
            priceLabel.textColor = UIColor(hex: "075125")
        }
    }

    func animateBid(_ value: Double) {
        contentView.backgroundColor = UIColor.yellow

        guard let stockItem = stockItem else { return }
        percentLabel.text = String(format: "%.1f%%", value + stockItem.percent)
        Utils.bounceView(percentLabel, for: 1)
    }
}
