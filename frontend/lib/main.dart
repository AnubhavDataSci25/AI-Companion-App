import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/router/app_router.dart';
import 'core/theme/ami_theme.dart';
import 'presentation/providers/theme_provider.dart';

void main() {
  runApp(const ProviderScope(child: AmiApp()));
}

class AmiApp extends ConsumerWidget {
  const AmiApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);

    return MaterialApp.router(
      title: 'Ami',
      debugShowCheckedModeBanner: false,
      theme: AmiTheme.light,
      darkTheme: AmiTheme.dark,
      themeMode: themeMode,
      routerConfig: appRouter,
    );
  }
}
