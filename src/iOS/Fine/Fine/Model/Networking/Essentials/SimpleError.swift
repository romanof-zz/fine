//
//  SimpleError.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import Foundation

public struct SimpleError: GenericError {
    let text: String

    public init(text: String) {
        self.text = text
    }

    public func localizedErrorDescription() -> String {
        return text
    }

    public func localizedErrorTitle() -> String {
        return NSLocalizedString("error.title", value: "Error", comment: "")
    }

    public static let generic = SimpleError(text: "error.generic.message")
}
