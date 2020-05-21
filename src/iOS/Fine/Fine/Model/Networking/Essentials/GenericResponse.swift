//
//  GenericResponse.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.
//

import Foundation

public enum GenericResponse <T> {
    case Success(T)
    case Error(GenericError)
}

public struct StatusResponse: Codable {
    public var status: String?

    public var isOk: Bool {
        return status == "ok"
    }
}
