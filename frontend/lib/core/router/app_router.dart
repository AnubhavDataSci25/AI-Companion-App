import 'package:go_router/go_router.dart';
import '../../presentation/screens/splash/splash_screen.dart';
import '../../presentation/screens/pin/pin_screen.dart';
import '../../presentation/screens/home/home_screen.dart';
import '../../presentation/screens/chat/chat_screen.dart';
import '../../presentation/screens/mood/mood_screen.dart';
import '../../presentation/screens/journal/journal_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/splash',
  routes: [
    GoRoute(path: '/splash', builder: (context, state) => const SplashScreen()),
    GoRoute(path: '/pin', builder: (context, state) => const PinScreen()),
    GoRoute(path: '/home', builder: (context, state) => const HomeScreen()),
    GoRoute(path: '/chat', builder: (context, state) => const ChatScreen()),
    GoRoute(path: '/mood', builder: (context, state) => const MoodScreen()),
    GoRoute(path: '/journal', builder: (context, state) => const JournalScreen()),
  ],
);