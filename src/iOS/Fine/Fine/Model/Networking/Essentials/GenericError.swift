//
//  GenericError.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//
//

import Foundation

public protocol GenericError: Error {
    func localizedErrorDescription() -> String
    func localizedErrorTitle() -> String
}
