import '../api/api_client.dart';

class JournalEntry {
  final String id;
  final String? title;
  final String content;
  final String? moodLabel;
  final DateTime createdAt;

  JournalEntry({
    required this.id,
    this.title,
    required this.content,
    this.moodLabel,
    required this.createdAt,
  });

  factory JournalEntry.fromJson(Map<String, dynamic> json) => JournalEntry(
        id: json['id'],
        title: json['title'],
        content: json['content'],
        moodLabel: json['mood_label'],
        createdAt: DateTime.parse(json['created_at']),
      );
}

class JournalRepository {
  final ApiClient _apiClient;
  JournalRepository(this._apiClient);

  Future<void> createEntry(String content, {String? title, String? moodLabel}) async {
    await _apiClient.dio.post('/journal/', data: {
      'title': title,
      'content': content,
      'mood_label': moodLabel,
    });
  }

  Future<List<JournalEntry>> getEntries() async {
    final response = await _apiClient.dio.get('/journal/');
    return (response.data as List).map((e) => JournalEntry.fromJson(e)).toList();
  }
}