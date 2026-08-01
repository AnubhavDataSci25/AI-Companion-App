import '../api/api_client.dart';

class MoodEntry {
  final String id;
  final String moodLabel;
  final double intensity;
  final String source;
  final String? note;
  final DateTime createdAt;

  MoodEntry({
    required this.id,
    required this.moodLabel,
    required this.intensity,
    required this.source,
    this.note,
    required this.createdAt,
  });

  factory MoodEntry.fromJson(Map<String, dynamic> json) => MoodEntry(
        id: json['id'],
        moodLabel: json['mood_label'],
        intensity: (json['intensity'] as num).toDouble(),
        source: json['source'],
        note: json['note'],
        createdAt: DateTime.parse(json['created_at']),
      );
}

class MoodRepository {
  final ApiClient _apiClient;
  MoodRepository(this._apiClient);

  Future<void> logMood(String moodLabel, double intensity, {String? note}) async {
    await _apiClient.dio.post('/mood/', data: {
      'mood_label': moodLabel,
      'intensity': intensity,
      'note': note,
    });
  }

  Future<List<MoodEntry>> getHistory() async {
    final response = await _apiClient.dio.get('/mood/');
    return (response.data as List).map((m) => MoodEntry.fromJson(m)).toList();
  }
}