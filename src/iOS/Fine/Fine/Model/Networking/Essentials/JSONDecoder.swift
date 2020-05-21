//
//  JSONDecoder.swift
//  Fine
//
//  Created by Valentyn Kovalsky on 16/05/2020.

import Foundation
import Alamofire

extension JSONDecoder {
  func decodeResponse<T: Decodable>(from response: DataResponse<Any>) -> GenericResponse<T> {
    guard response.error == nil else {
      print(response.error!)
        return .Error(NetworkError(type:.generic))
    }

    guard let responseData = response.data else {
      return .Error(NetworkError(type:.parsing))
    }

    do {
      let item = try decode(T.self, from: responseData)
      return .Success(item)
    } catch {
      return .Error(NetworkError(type:.generic))
    }
  }
}
