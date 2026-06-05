import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'theme.dart';

class HomeScreen extends StatefulWidget {
  final VoidCallback? onContactTap;
  const HomeScreen({super.key, this.onContactTap});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late VideoPlayerController _controller;
  bool _initialized = false;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.asset('assets/videos/casona_final.mp4')
      ..setLooping(true)
      ..setVolume(0)
      ..initialize().then((_) {
        if (mounted) {
          setState(() => _initialized = true);
          _controller.play();
        }
      });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;
    final heroHeight = isMobile ? 480.0 : 520.0;
    final titleSize = isMobile ? 42.0 : 68.0;

    return Stack(
      children: [
        // Video hero (fallback a imagen mientras carga)
        SizedBox(
          height: heroHeight,
          width: double.infinity,
          child: _initialized
              ? FittedBox(
                  fit: BoxFit.cover,
                  clipBehavior: Clip.hardEdge,
                  child: SizedBox(
                    width: _controller.value.size.width,
                    height: _controller.value.size.height,
                    child: VideoPlayer(_controller),
                  ),
                )
              : Image.asset(
                  'assets/images/hero.jpg',
                  fit: BoxFit.cover,
                  cacheWidth: 1400,
                ),
        ),
        // Gradiente oscuro
        Container(
          height: heroHeight,
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Color(0x77000000),
                Color(0xCC000000),
              ],
            ),
          ),
        ),
        // Contenido centrado
        SizedBox(
          height: heroHeight,
          child: Center(
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: isMobile ? 24 : 40),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Línea decorativa + label
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: Colors.black.withValues(alpha: 0.35),
                      borderRadius: BorderRadius.circular(2),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(width: isMobile ? 24 : 40, height: 1, color: AppTheme.gold),
                        const SizedBox(width: 12),
                        Text(
                          'CENTRO DE EVENTOS · CHILE',
                          style: TextStyle(
                            color: AppTheme.gold,
                            fontSize: isMobile ? 9 : 11,
                            letterSpacing: isMobile ? 2.5 : 3.5,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Container(width: isMobile ? 24 : 40, height: 1, color: AppTheme.gold),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  Text(
                    'Casona Fundo\nEl Castillo',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.displayLarge?.copyWith(
                          color: Colors.white,
                          fontSize: titleSize,
                          height: 1.05,
                          shadows: const [
                            Shadow(
                              color: Color(0x88000000),
                              blurRadius: 20,
                              offset: Offset(0, 4),
                            ),
                          ],
                        ),
                  ),
                  const SizedBox(height: 14),
                  Text(
                    'Historia, naturaleza y elegancia\nen un parque francés centenario.',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: const Color(0xCCFFFFFF),
                      fontSize: isMobile ? 14 : 16,
                      height: 1.6,
                      letterSpacing: 0.3,
                    ),
                  ),
                  const SizedBox(height: 28),
                  OutlinedButton(
                    onPressed: widget.onContactTap,
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.white,
                      side: const BorderSide(color: AppTheme.gold, width: 1.5),
                      padding: EdgeInsets.symmetric(
                        horizontal: isMobile ? 24 : 36,
                        vertical: 14,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(4),
                      ),
                    ),
                    child: Text(
                      'SOLICITAR INFORMACIÓN',
                      style: TextStyle(
                        fontSize: isMobile ? 11 : 12,
                        letterSpacing: 2,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}
