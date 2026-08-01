import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../providers/app_providers.dart';

const _moodOptions = {
  'happy': '😊',
  'content': '🙂',
  'excited': '🤩',
  'neutral': '😐',
  'tired': '😴',
  'stressed': '😣',
  'anxious': '😟',
  'sad': '😢',
  'lonely': '🥺',
  'angry': '😠',
};

class MoodScreen extends ConsumerStatefulWidget {
  const MoodScreen({super.key});

  @override
  ConsumerState<MoodScreen> createState() => _MoodScreenState();
}

class _MoodScreenState extends ConsumerState<MoodScreen> {
  bool _logging = false;

  Future<void> _logMood(String label) async {
    setState(() => _logging = true);
    try {
      await ref.read(moodRepositoryProvider).logMood(label, 0.7);
      ref.invalidate(moodHistoryProvider);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Mood logged 💜')),
        );
      }
    } finally {
      if (mounted) setState(() => _logging = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final historyAsync = ref.watch(moodHistoryProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Mood Tracker')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('How are you feeling?', style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: _moodOptions.entries.map((entry) {
                    return ActionChip(
                      avatar: Text(entry.value, style: const TextStyle(fontSize: 18)),
                      label: Text(entry.key),
                      onPressed: _logging ? null : () => _logMood(entry.key),
                    );
                  }).toList(),
                ),
              ],
            ),
          ),
          const Divider(),
          Expanded(
            child: historyAsync.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => const Center(child: Text('Could not load mood history.')),
              data: (entries) {
                if (entries.isEmpty) {
                  return const Center(child: Text('No mood entries yet.'));
                }
                return ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: entries.length,
                  itemBuilder: (context, index) {
                    final e = entries[index];
                    return Card(
                      child: ListTile(
                        leading: Text(_moodOptions[e.moodLabel] ?? '💭', style: const TextStyle(fontSize: 22)),
                        title: Text(e.moodLabel),
                        subtitle: Text(DateFormat('MMM d, h:mm a').format(e.createdAt.toLocal())),
                        trailing: Text(e.source == 'chat' ? 'auto' : 'logged',
                            style: Theme.of(context).textTheme.bodySmall),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}