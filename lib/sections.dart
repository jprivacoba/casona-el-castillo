import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:photo_view/photo_view.dart';
import 'package:photo_view/photo_view_gallery.dart';
import 'package:url_launcher/url_launcher.dart';
import 'theme.dart';

class AboutSection extends StatelessWidget {
  const AboutSection({super.key});

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Container(
      color: AppTheme.cream,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 72,
        horizontal: isMobile ? 20 : 40,
      ),
      child: isMobile ? _buildMobile(context) : _buildDesktop(context),
    );
  }

  Widget _buildDesktop(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Expanded(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.asset(
              'assets/images/quienes-somos.jpg',
              height: 380,
              fit: BoxFit.cover,
              cacheWidth: 700,
            ),
          ),
        ),
        const SizedBox(width: 56),
        Expanded(child: _buildText(context)),
      ],
    );
  }

  Widget _buildMobile(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: Image.asset(
            'assets/images/quienes-somos.jpg',
            height: 240,
            width: double.infinity,
            fit: BoxFit.cover,
            cacheWidth: 700,
          ),
        ),
        const SizedBox(height: 32),
        _buildText(context),
      ],
    );
  }

  Widget _buildText(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _sectionLabel('QUIÉNES SOMOS'),
        const SizedBox(height: 16),
        Text(
          'Nuestra Historia',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
        const SizedBox(height: 8),
        Container(width: 48, height: 2, color: AppTheme.gold),
        const SizedBox(height: 24),
        Text(
          'Casona Fundo El Castillo nace del sueño familiar de devolverle vida a un parque con más de 80 años de historia. Diseñado por un paisajista francés y rodeado de árboles centenarios, este lugar único combina patrimonio, naturaleza y elegancia.',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
        const SizedBox(height: 16),
        Text(
          'Nuestra antigua casona ha sido cuidadosamente restaurada, integrando modernos baños y una cocina de más de 300 m², creando el escenario perfecto para eventos inolvidables.',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
      ],
    );
  }
}

class LocationSection extends StatefulWidget {
  const LocationSection({super.key});

  @override
  State<LocationSection> createState() => _LocationSectionState();
}

class _LocationSectionState extends State<LocationSection> {
  static final LatLng _location = LatLng(-32.8850, -70.6494);
  final MapController _mapController = MapController();

  void _openInMaps() {
    final uri = Uri.parse(
      'https://www.google.com/maps/search/?api=1&query=${_location.latitude},${_location.longitude}',
    );
    launchUrl(uri, mode: LaunchMode.externalApplication);
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Container(
      color: AppTheme.creamAlt,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 72,
        horizontal: isMobile ? 20 : 40,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _sectionLabel('UBICACIÓN'),
          const SizedBox(height: 16),
          Text(
            'Dónde encontrarnos',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Container(width: 48, height: 2, color: AppTheme.gold),
          const SizedBox(height: 32),
          if (isMobile) _buildMobile() else _buildDesktop(),
        ],
      ),
    );
  }

  Widget _buildDesktop() {
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            flex: 3,
            child: _buildMap(isMobile: false),
          ),
          const SizedBox(width: 32),
          Expanded(
            flex: 2,
            child: _buildInfoCard(),
          ),
        ],
      ),
    );
  }

  Widget _buildMobile() {
    return Column(
      children: [
        _buildMap(isMobile: true),
        const SizedBox(height: 16),
        _buildInfoCard(),
      ],
    );
  }

  Widget _buildMap({required bool isMobile}) {
    // Móvil: solo dos dedos (un dedo hace scroll de página)
    // Desktop: scroll wheel + drag completo
    final interactionFlags = isMobile
        ? InteractiveFlag.pinchZoom |
          InteractiveFlag.pinchMove |
          InteractiveFlag.doubleTapZoom
        : InteractiveFlag.scrollWheelZoom |
          InteractiveFlag.pinchZoom |
          InteractiveFlag.drag |
          InteractiveFlag.doubleTapZoom;

    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: SizedBox(
        height: isMobile ? 240 : 340,
        child: Stack(
          children: [
            FlutterMap(
              mapController: _mapController,
              options: MapOptions(
                initialCenter: _location,
                initialZoom: 14,
                interactionOptions: InteractionOptions(
                  flags: interactionFlags,
                ),
              ),
              children: [
                TileLayer(
                  // ESRI World Topo Map (terrain)
                  urlTemplate:
                      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
                  userAgentPackageName: 'com.casona.app',
                ),
                MarkerLayer(
                  markers: [
                    Marker(
                      point: _location,
                      width: 48,
                      height: 56,
                      child: GestureDetector(
                        onTap: _openInMaps,
                        child: const _MapPin(),
                      ),
                    ),
                  ],
                ),
              ],
            ),
            // Botones de zoom (solo desktop)
            if (!isMobile)
              Positioned(
                right: 12,
                bottom: 24,
                child: _ZoomButtons(controller: _mapController),
              ),
            // Indicador móvil
            if (isMobile)
              Positioned(
                bottom: 8,
                left: 0,
                right: 0,
                child: Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.black54,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'Usa dos dedos para mover el mapa',
                      style: TextStyle(color: Colors.white70, fontSize: 11),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard() {
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        color: AppTheme.white,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFFE0D5C5)),
      ),
      padding: const EdgeInsets.symmetric(vertical: 32, horizontal: 24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.location_on, size: 40, color: AppTheme.gold),
          const SizedBox(height: 16),
          const Text(
            'Calle Larga',
            style: TextStyle(
              fontSize: 20,
              fontFamily: 'Playfair Display',
              fontWeight: FontWeight.w600,
              color: AppTheme.dark,
            ),
          ),
          const SizedBox(height: 6),
          const Text(
            'Los Andes, Valparaíso',
            style: TextStyle(color: AppTheme.muted, fontSize: 14),
          ),
          const SizedBox(height: 24),
          const Divider(indent: 32, endIndent: 32, color: Color(0xFFE0D5C5)),
          const SizedBox(height: 24),
          const Text(
            'A 80 km de Santiago.\nAcceso fácil por Ruta 60.',
            textAlign: TextAlign.center,
            style: TextStyle(color: AppTheme.muted, fontSize: 13, height: 1.7),
          ),
          const SizedBox(height: 20),
          OutlinedButton.icon(
            onPressed: _openInMaps,
            icon: const Icon(Icons.map_outlined, size: 16),
            label: const Text('Abrir en Google Maps'),
            style: OutlinedButton.styleFrom(
              foregroundColor: AppTheme.dark,
              side: const BorderSide(color: AppTheme.gold),
              textStyle: const TextStyle(fontSize: 12, letterSpacing: 0.5),
            ),
          ),
        ],
      ),
    );
  }
}

class _ZoomButtons extends StatelessWidget {
  final MapController controller;
  const _ZoomButtons({required this.controller});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _ZoomButton(
          icon: Icons.add,
          onTap: () => controller.move(
            controller.camera.center,
            controller.camera.zoom + 1,
          ),
        ),
        const SizedBox(height: 4),
        _ZoomButton(
          icon: Icons.remove,
          onTap: () => controller.move(
            controller.camera.center,
            controller.camera.zoom - 1,
          ),
        ),
      ],
    );
  }
}

class _ZoomButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;
  const _ZoomButton({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 32,
        height: 32,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(4),
          boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 4)],
        ),
        child: Icon(icon, size: 18, color: AppTheme.dark),
      ),
    );
  }
}

class _MapPin extends StatelessWidget {
  const _MapPin();

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 36,
          height: 36,
          decoration: const BoxDecoration(
            color: AppTheme.gold,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(color: Colors.black26, blurRadius: 6, offset: Offset(0, 3)),
            ],
          ),
          child: const Icon(Icons.villa_outlined, color: Colors.white, size: 20),
        ),
        CustomPaint(
          size: const Size(12, 8),
          painter: _TrianglePainter(),
        ),
      ],
    );
  }
}

class _TrianglePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = AppTheme.gold;
    final path = ui.Path()
      ..moveTo(0, 0)
      ..lineTo(size.width, 0)
      ..lineTo(size.width / 2, size.height)
      ..close();
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(_) => false;
}

// ─── Historia & Eventos ──────────────────────────────────────────────────────

class HistoriaEventosSection extends StatefulWidget {
  const HistoriaEventosSection({super.key});

  @override
  State<HistoriaEventosSection> createState() => _HistoriaEventosSectionState();
}

class _HistoriaEventosSectionState extends State<HistoriaEventosSection>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  static const List<String> _historia = [
    'assets/images/imagenes/historia/WhatsApp Image 2026-03-09 at 13.01.59.jpeg',
    'assets/images/imagenes/historia/WhatsApp Image 2026-03-09 at 13.02.00.jpeg',
    'assets/images/imagenes/historia/WhatsApp Image 2026-03-09 at 13.02.03.jpeg',
    'assets/images/imagenes/historia/WhatsApp Image 2026-03-09 at 13.02.04.jpeg',
    'assets/images/imagenes/historia/WhatsApp Image 2026-03-09 at 13.02.07.jpeg',
  ];

  static const List<String> _carpa = [
    'assets/images/carpa/carpa1.jpeg',
    'assets/images/carpa/carpa2.jpeg',
    'assets/images/carpa/carpa3.jpeg',
    'assets/images/carpa/carpa4.jpeg',
  ];

  static const List<String> _eventos = [
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 12.58.04.jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.52.jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.53 (2).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.53.jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.54 (1).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.54.jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.55 (1).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.55 (2).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.03.55.jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.04.50 (1).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.04.50 (2).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.04.50.jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.04.51 (1).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.04.51 (2).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.04.51 (3).jpeg',
    'assets/images/imagenes/eventos/WhatsApp Image 2026-03-09 at 13.04.52 (1).jpeg',
  ];

  int _selectedTab = 0;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _tabController.addListener(() {
      if (!_tabController.indexIsChanging) {
        setState(() => _selectedTab = _tabController.index);
      }
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;
    final images = _selectedTab == 0 ? _eventos : (_selectedTab == 1 ? _historia : _carpa);

    return Container(
      color: AppTheme.cream,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 72,
        horizontal: isMobile ? 16 : 40,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(context),
          const SizedBox(height: 28),
          _buildTabBar(),
          const SizedBox(height: 24),
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 250),
            child: KeyedSubtree(
              key: ValueKey(_selectedTab),
              child: _PhotoGrid(
                      images: images,
                      isMobile: isMobile,
                      videos: _selectedTab == 0
                          ? [
                              (videoPath: 'assets/videos/video-eventos.mp4', previewPath: 'assets/images/video-preview.jpg'),
                              (videoPath: 'assets/videos/video-eventos-2.mp4', previewPath: 'assets/images/video-preview-2.jpg'),
                            ]
                          : null,
                    ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(width: 32, height: 1.5, color: AppTheme.gold),
            const SizedBox(width: 10),
            const Text(
              'FOTOGRAFÍAS',
              style: TextStyle(
                fontSize: 11,
                letterSpacing: 2.5,
                color: AppTheme.gold,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
        const SizedBox(height: 14),
        Text('Historia y Eventos', style: Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height: 6),
        Container(width: 48, height: 2, color: AppTheme.gold),
        const SizedBox(height: 8),
        const Text(
          'Un recorrido visual por nuestra casona y los momentos que la hacen única.',
          style: TextStyle(color: AppTheme.muted, fontSize: 13, height: 1.6),
        ),
      ],
    );
  }

  Widget _buildTabBar() {
    return Container(
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: Color(0xFFE0D5C5), width: 1.5)),
      ),
      child: TabBar(
        controller: _tabController,
        isScrollable: false,
        labelColor: AppTheme.dark,
        unselectedLabelColor: AppTheme.muted,
        indicatorColor: AppTheme.gold,
        indicatorWeight: 2,
        labelStyle: const TextStyle(
          fontSize: 13,
          fontWeight: FontWeight.w600,
          letterSpacing: 1.2,
        ),
        unselectedLabelStyle: const TextStyle(
          fontSize: 13,
          fontWeight: FontWeight.w400,
          letterSpacing: 1.2,
        ),
        tabs: [
          Tab(text: 'EVENTOS  (${_eventos.length})'),
          Tab(text: 'HISTORIA  (${_historia.length})'),
          Tab(text: 'EVENTOS EN CARPA  (${_carpa.length})'),
        ],
      ),
    );
  }
}


class _PhotoGrid extends StatelessWidget {
  final List<String> images;
  final bool isMobile;
  final List<({String videoPath, String previewPath})>? videos;

  const _PhotoGrid({required this.images, required this.isMobile, this.videos});

  @override
  Widget build(BuildContext context) {
    final videoCount = videos?.length ?? 0;
    final totalCount = images.length + videoCount;

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: isMobile ? 2 : 3,
        crossAxisSpacing: isMobile ? 6 : 8,
        mainAxisSpacing: isMobile ? 6 : 8,
        childAspectRatio: 1.1,
      ),
      itemCount: totalCount,
      itemBuilder: (context, index) {
        if (index < videoCount) {
          final v = videos![index];
          return _VideoTile(videoPath: v.videoPath, previewPath: v.previewPath);
        }
        final imgIndex = index - videoCount;
        return GestureDetector(
          onTap: () => _openViewer(context, imgIndex),
          child: Hero(
            tag: images[imgIndex],
            child: ClipRRect(
              borderRadius: BorderRadius.circular(6),
              child: Image.asset(
                images[imgIndex],
                fit: BoxFit.cover,
                cacheWidth: 400,
              ),
            ),
          ),
        );
      },
    );
  }

  void _openViewer(BuildContext context, int initialIndex) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => _FullscreenViewer(images: images, initialIndex: initialIndex),
      ),
    );
  }
}

class _VideoTile extends StatelessWidget {
  final String videoPath;
  final String previewPath;
  const _VideoTile({required this.videoPath, required this.previewPath});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => showDialog(
        context: context,
        builder: (_) => _VideoDialog(videoPath: videoPath),
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(6),
        child: Stack(
          fit: StackFit.expand,
          children: [
            Image.asset(
              previewPath,
              fit: BoxFit.cover,
            ),
            Container(color: Colors.black38),
            const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.play_circle_outline, color: AppTheme.gold, size: 40),
                  SizedBox(height: 8),
                  Text(
                    'VER VIDEO',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 11,
                      letterSpacing: 1.5,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _VideoDialog extends StatefulWidget {
  final String videoPath;
  const _VideoDialog({required this.videoPath});

  @override
  State<_VideoDialog> createState() => _VideoDialogState();
}

class _VideoDialogState extends State<_VideoDialog> {
  late VideoPlayerController _controller;
  bool _initialized = false;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.asset(widget.videoPath)
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
    return Dialog(
      backgroundColor: Colors.black,
      insetPadding: const EdgeInsets.all(16),
      child: Stack(
        children: [
          _initialized
              ? AspectRatio(
                  aspectRatio: _controller.value.aspectRatio,
                  child: GestureDetector(
                    onTap: () => setState(() {
                      _controller.value.isPlaying
                          ? _controller.pause()
                          : _controller.play();
                    }),
                    child: VideoPlayer(_controller),
                  ),
                )
              : const AspectRatio(
                  aspectRatio: 16 / 9,
                  child: Center(
                    child: CircularProgressIndicator(color: AppTheme.gold),
                  ),
                ),
          Positioned(
            top: 8,
            right: 8,
            child: GestureDetector(
              onTap: () => Navigator.pop(context),
              child: Container(
                decoration: const BoxDecoration(
                  color: Colors.black54,
                  shape: BoxShape.circle,
                ),
                padding: const EdgeInsets.all(4),
                child: const Icon(Icons.close, color: Colors.white, size: 20),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _FullscreenViewer extends StatefulWidget {
  final List<String> images;
  final int initialIndex;

  const _FullscreenViewer({required this.images, required this.initialIndex});

  @override
  State<_FullscreenViewer> createState() => _FullscreenViewerState();
}

class _FullscreenViewerState extends State<_FullscreenViewer> {
  late int _current;
  late PageController _pageController;

  @override
  void initState() {
    super.initState();
    _current = widget.initialIndex;
    _pageController = PageController(initialPage: widget.initialIndex);
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  void _goTo(int index) {
    if (index < 0 || index >= widget.images.length) return;
    _pageController.animateToPage(
      index,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeInOut,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        title: Text(
          '${_current + 1} / ${widget.images.length}',
          style: const TextStyle(color: Colors.white54, fontSize: 14, letterSpacing: 1),
        ),
      ),
      body: Stack(
        children: [
          PhotoViewGallery.builder(
            scrollPhysics: const ClampingScrollPhysics(),
            builder: (context, index) => PhotoViewGalleryPageOptions(
              imageProvider: AssetImage(widget.images[index]),
              initialScale: PhotoViewComputedScale.contained,
              heroAttributes: PhotoViewHeroAttributes(tag: widget.images[index]),
            ),
            itemCount: widget.images.length,
            loadingBuilder: (context, event) => const Center(
              child: CircularProgressIndicator(color: Colors.white38),
            ),
            pageController: _pageController,
            onPageChanged: (index) => setState(() => _current = index),
          ),
          if (_current > 0)
            Positioned(
              left: 16,
              top: 0,
              bottom: 0,
              child: Center(
                child: _NavBtn(icon: Icons.chevron_left, onTap: () => _goTo(_current - 1)),
              ),
            ),
          if (_current < widget.images.length - 1)
            Positioned(
              right: 16,
              top: 0,
              bottom: 0,
              child: Center(
                child: _NavBtn(icon: Icons.chevron_right, onTap: () => _goTo(_current + 1)),
              ),
            ),
        ],
      ),
    );
  }
}

class _NavBtn extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;
  const _NavBtn({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 48,
        height: 48,
        decoration: BoxDecoration(
          color: Colors.black54,
          shape: BoxShape.circle,
          border: Border.all(color: Colors.white24),
        ),
        child: Icon(icon, color: Colors.white, size: 28),
      ),
    );
  }
}

// ─── Shared label ─────────────────────────────────────────────────────────────

Widget _sectionLabel(String text) {
  return Text(
    text,
    style: const TextStyle(
      fontSize: 11,
      letterSpacing: 2.5,
      color: AppTheme.gold,
      fontWeight: FontWeight.w700,
    ),
  );
}
