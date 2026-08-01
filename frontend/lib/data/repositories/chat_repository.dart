import '../api/api_client.dart';

class ChatMessage {
  final String sender; // "user" or "ami"
  final String content;
  final String? mood;

  ChatMessage({required this.sender, required this.content, this.mood});

  factory ChatMessage.fromJson(Map<String, dynamic> json) => ChatMessage(
        sender: json['sender'],
        content: json['content'],
        mood: json['mood'],
      );
}

class ChatRepository {
  final ApiClient _apiClient;

  ChatRepository(this._apiClient);

  /// Sends a message, returns (conversationId, replyText).
  Future<(String, String)> sendMessage(String? conversationId, String message) async {
    final response = await _apiClient.dio.post('/chat/send', data: {
      'conversation_id': conversationId,
      'message': message,
    });
    return (response.data['conversation_id'] as String, response.data['reply'] as String);
  }

  Future<List<ChatMessage>> getMessages(String conversationId) async {
    final response = await _apiClient.dio.get('/chat/$conversationId/messages');
    final list = response.data as List;
    return list.map((m) => ChatMessage.fromJson(m)).toList();
  }
}