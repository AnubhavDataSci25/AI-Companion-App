import 'package:dio/dio.dart';
import '../../core/constants/api_constants.dart';
import '../../core/services/secure_storage_service.dart';

class ApiClient {
  final Dio dio;
  final SecureStorageService _storage;

  ApiClient(this._storage)
      : dio = Dio(BaseOptions(
          baseUrl: ApiConstants.baseUrl,
          connectTimeout: const Duration(seconds: 15),
          receiveTimeout: const Duration(seconds: 30),
        )) {
    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _storage.getToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
    ));
  }
}