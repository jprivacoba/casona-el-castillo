import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'theme.dart';
import 'home_screen.dart';
import 'gallery_screen.dart';
import 'menu_screen.dart';
import 'contact_screen.dart';
import 'sections.dart';

void main() {
  runApp(const CasonaApp());
}

class CasonaApp extends StatelessWidget {
  const CasonaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Casona Fundo El Castillo',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      scrollBehavior: const MaterialScrollBehavior().copyWith(
        dragDevices: {
          PointerDeviceKind.mouse,
          PointerDeviceKind.touch,
          PointerDeviceKind.trackpad,
        },
      ),
      home: const MainNavigation(),
    );
  }
}

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  final ScrollController _scrollController = ScrollController();

  final GlobalKey _homeKey = GlobalKey();
  final GlobalKey _aboutKey = GlobalKey();
  final GlobalKey _historiaEventosKey = GlobalKey();
  final GlobalKey _galleryKey = GlobalKey();
  final GlobalKey _menuKey = GlobalKey();
  final GlobalKey _locationKey = GlobalKey();
  final GlobalKey _contactKey = GlobalKey();

  void _scrollToSection(GlobalKey key) {
    final ctx = key.currentContext;
    if (ctx != null) {
      Scrollable.ensureVisible(
        ctx,
        duration: const Duration(milliseconds: 700),
        curve: Curves.easeInOut,
      );
    }
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Scaffold(
      backgroundColor: AppTheme.cream,
      drawer: isMobile ? _buildDrawer(context) : null,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(64),
        child: Builder(
          builder: (ctx) => Container(
            decoration: const BoxDecoration(
              color: AppTheme.cream,
              border: Border(
                bottom: BorderSide(color: Color(0xFFE8DDD0), width: 1),
              ),
            ),
            child: SafeArea(
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: isMobile ? 16 : 32),
                child: Row(
                  children: [
                    GestureDetector(
                      onTap: () => _scrollToSection(_homeKey),
                      child: Image.asset(
                        'assets/images/logo.png',
                        height: 48,
                      ),
                    ),
                    const Spacer(),
                    if (isMobile)
                      IconButton(
                        icon: const Icon(Icons.menu, color: AppTheme.dark),
                        onPressed: () => Scaffold.of(ctx).openDrawer(),
                      )
                    else ...[
                      _navItem('Inicio', _homeKey),
                      _navItem('Quiénes Somos', _aboutKey),
                      _navItem('Galería', _galleryKey),
                      _navItem('Historia y Eventos', _historiaEventosKey),
                      _navItem('Ubicación', _locationKey),
                      _navItem('Menú', _menuKey),
                      _navItem('Contacto', _contactKey),
                    ],
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
      body: SingleChildScrollView(
        controller: _scrollController,
        physics: const BouncingScrollPhysics(parent: AlwaysScrollableScrollPhysics()),
        child: Column(
          children: [
            HomeScreen(key: _homeKey, onContactTap: () => _scrollToSection(_contactKey)),
            AboutSection(key: _aboutKey),
            GallerySection(key: _galleryKey),
            HistoriaEventosSection(key: _historiaEventosKey),
            LocationSection(key: _locationKey),
            MenuScreen(key: _menuKey),
            ContactSection(key: _contactKey),
            _buildFooter(),
          ],
        ),
      ),
    );
  }

  Widget _buildDrawer(BuildContext context) {
    return Drawer(
      backgroundColor: AppTheme.cream,
      child: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
              child: Image.asset('assets/images/logo.png', height: 56),
            ),
            const Divider(color: Color(0xFFE8DDD0), height: 1),
            const SizedBox(height: 8),
            _drawerItem(context, 'Inicio', _homeKey),
            _drawerItem(context, 'Quiénes Somos', _aboutKey),
            _drawerItem(context, 'Galería', _galleryKey),
            _drawerItem(context, 'Historia y Eventos', _historiaEventosKey),
            _drawerItem(context, 'Ubicación', _locationKey),
            _drawerItem(context, 'Menú', _menuKey),
            _drawerItem(context, 'Contacto', _contactKey),
          ],
        ),
      ),
    );
  }

  Widget _drawerItem(BuildContext context, String title, GlobalKey key) {
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 2),
      title: Text(
        title,
        style: const TextStyle(
          fontSize: 15,
          fontWeight: FontWeight.w500,
          color: AppTheme.text,
          letterSpacing: 0.3,
        ),
      ),
      onTap: () {
        Navigator.pop(context);
        Future.delayed(
          const Duration(milliseconds: 300),
          () => _scrollToSection(key),
        );
      },
    );
  }

  Widget _navItem(String title, GlobalKey key) {
    return TextButton(
      onPressed: () => _scrollToSection(key),
      style: TextButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        foregroundColor: AppTheme.text,
      ),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 13,
          fontWeight: FontWeight.w500,
          letterSpacing: 0.3,
        ),
      ),
    );
  }

  Widget _buildFooter() {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 48, horizontal: 32),
      width: double.infinity,
      color: AppTheme.dark,
      child: Column(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.asset(
              'assets/images/logo.png',
              height: 100,
            ),
          ),
          const SizedBox(height: 24),
          const Text(
            'Calle Larga, Los Andes · Valparaíso, Chile',
            textAlign: TextAlign.center,
            style: TextStyle(color: Color(0xFFBBB3AA), fontSize: 14),
          ),
          const SizedBox(height: 4),
          const Text(
            'casonaelcastillo1933@gmail.com',
            textAlign: TextAlign.center,
            style: TextStyle(color: Color(0xFFBBB3AA), fontSize: 14),
          ),
          const SizedBox(height: 28),
          const Text(
            '© 2026 Casona Fundo El Castillo · Todos los derechos reservados',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 11, color: Color(0xFF6A6058)),
          ),
        ],
      ),
    );
  }
}

class GallerySection extends StatelessWidget {
  const GallerySection({super.key});

  @override
  Widget build(BuildContext context) {
    return const GalleryScreen();
  }
}
