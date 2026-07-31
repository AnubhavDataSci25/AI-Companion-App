import 'package:dio/dio.dart';
import '../api/api_client.dart';
import '../../core/services/secure_storage_service.dart';

class AuthRepository {
  final ApiClient _apiClient;
  final SecureStorageService _storage;

  AuthRepository(this._apiClient, this._storage);

  /// Returns null on success, or an error message string on failure.
  Future<String?> login(String name, String pin) async {
    try {
      final response = await _apiClient.dio.post('/auth/login', data: {
        'name': name,
        'pin': pin,
      });
      final token = response.data['token'] as String;
      final role = response.data['role'] as String;
      await _storage.saveSession(token, role);
      return null;
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        return 'Incorrect name or PIN.';
      }
      if (e.response?.statusCode == 429) {
        return 'Too many attempts. Please wait a moment.';
      }
      if (e.type == DioExceptionType.connectionTimeout ||
          e.type == DioExceptionType.connectionError) {
        return "Can't reach Ami's server. Check your connection.";
      }
      return 'Something went wrong. Please try again.';
    }
  }

  Future<bool> isLoggedIn() async {
    final token = await _storage.getToken();
    return token != null;
  }

  Future<void> logout() async {
    await _storage.clearSession();
  }
}