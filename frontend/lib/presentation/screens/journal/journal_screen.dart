import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../providers/app_providers.dart';

class JournalScreen extends ConsumerWidget {
  const JournalScreen({super.key});

  void _openNewEntrySheet(BuildContext context, WidgetRef ref) {
    final controller = TextEditingController();
    final titleController = TextEditingController();

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => Padding(
        padding: EdgeInsets.only(
          left: 16, right: 16, top: 16,
          bottom: MediaQuery.of(context).viewInsets.bottom + 16,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('New Journal Entry', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 12),
            TextField(
              controller: titleController,
              decoration: const InputDecoration(hintText: 'Title (optional)'),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: controller,
              maxLines: 5,
              decoration: const InputDecoration(hintText: "What's on your mind?"),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () async {
                if (controller.text.trim().isEmpty) return;
                await ref.read(journalRepositoryProvider).createEntry(
                      controller.text.trim(),
                      title: titleController.text.trim().isEmpty ? null : titleController.text.trim(),
                    );
                ref.invalidate(journalEntriesProvider);
                if (context.mounted) Navigator.pop(context);
              },
              child: const Text('Save Entry'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final entriesAsync = ref.watch(journalEntriesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Journal')),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _openNewEntrySheet(context, ref),
        child: const Icon(Icons.add),
      ),
      body: entriesAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => const Center(child: Text('Could not load journal entries.')),
        data: (entries) {
          if (entries.isEmpty) {
            return const Center(child: Text('No journal entries yet. Tap + to write one.'));
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: entries.length,
            itemBuilder: (context, index) {
              final e = entries[index];
              return Card(
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (e.title != null)
                        Text(e.title!, style: Theme.of(context).textTheme.titleSmall),
                      const SizedBox(height: 4),
                      Text(e.content),
                      const SizedBox(height: 6),
                      Text(
                        DateFormat('MMM d, yyyy • h:mm a').format(e.createdAt.toLocal()),
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}