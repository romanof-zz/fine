//
//  NetworkManager.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.

import Foundation

public struct NetworkManager {
    
    private let baseURL: String
    private let api: String
     public let middleware: NetworkMiddleware
    
    public init(baseUrl: String, api: String) {
        self.baseURL = baseUrl
        self.api = api
        self.middleware = NetworkMiddleware(baseURL: baseURL, apiVersion: api)
    }
}
