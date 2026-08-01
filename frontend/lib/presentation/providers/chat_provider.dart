import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/chat_repository.dart';
import 'app_providers.dart';

class ChatState {
  final List<ChatMessage> messages;
  final String? conversationId;
  final bool sending;
  final String? error;

  ChatState({this.messages = const [], this.conversationId, this.sending = false, this.error});

  ChatState copyWith({
    List<ChatMessage>? messages,
    String? conversationId,
    bool? sending,
    String? error,
  }) =>
      ChatState(
        messages: messages ?? this.messages,
        conversationId: conversationId ?? this.conversationId,
        sending: sending ?? this.sending,
        error: error,
      );
}

class ChatNotifier extends StateNotifier<ChatState> {
  final ChatRepository _repo;

  ChatNotifier(this._repo) : super(ChatState());

  Future<void> sendMessage(String text) async {
    // Optimistically show the user's message immediately
    state = state.copyWith(
      messages: [...state.messages, ChatMessage(sender: 'user', content: text)],
      sending: true,
      error: null,
    );

    try {
      final (conversationId, reply) = await _repo.sendMessage(state.conversationId, text);
      state = state.copyWith(
        conversationId: conversationId,
        messages: [...state.messages, ChatMessage(sender: 'ami', content: reply)],
        sending: false,
      );
    } catch (e) {
      state = state.copyWith(sending: false, error: "Ami couldn't respond. Please try again.");
    }
  }
}

final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>(
  (ref) => ChatNotifier(ref.watch(chatRepositoryProvider)),
);