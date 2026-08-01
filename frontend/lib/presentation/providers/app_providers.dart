import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/services/secure_storage_service.dart';
import '../../data/api/api_client.dart';
import '../../data/repositories/auth_repository.dart';
import '../../data/repositories/chat_repository.dart';
import '../../data/repositories/mood_repository.dart';
import '../../data/repositories/journal_repository.dart';

final secureStorageProvider = Provider((ref) => SecureStorageService());

final apiClientProvider = Provider((ref) => ApiClient(ref.watch(secureStorageProvider)));

final authRepositoryProvider = Provider(
  (ref) => AuthRepository(ref.watch(apiClientProvider), ref.watch(secureStorageProvider)),
);

final chatRepositoryProvider = Provider(
  (ref) => ChatRepository(ref.watch(apiClientProvider)),
);

final moodRepositoryProvider = Provider(
  (ref) => MoodRepository(ref.watch(apiClientProvider)),
);
 
final journalRepositoryProvider = Provider(
  (ref) => JournalRepository(ref.watch(apiClientProvider)),
);

final moodHistoryProvider = FutureProvider.autoDispose((ref) {
  return ref.watch(moodRepositoryProvider).getHistory();
});

final journalEntriesProvider = FutureProvider.autoDispose((ref) {
  return ref.watch(journalRepositoryProvider).getEntries();
});