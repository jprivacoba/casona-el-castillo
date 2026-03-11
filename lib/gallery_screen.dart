import 'package:flutter/material.dart';
import 'package:photo_view/photo_view.dart';
import 'package:photo_view/photo_view_gallery.dart';
import 'theme.dart';

class GalleryScreen extends StatelessWidget {
  const GalleryScreen({super.key});

  static const List<String> _images = [
    'assets/images/hero.jpg',
    'assets/images/quienes-somos.jpg',
    'assets/images/ubicacion.jpg',
    'assets/images/foto pack.jpg',
    'assets/images/img2.jpg',
    'assets/images/img3.jpg',
    'assets/images/img4.jpg',
    'assets/images/img5.jpg',
    'assets/images/img6.jpg',
    'assets/images/img7.jpg',
    'assets/images/img8.jpg',
    'assets/images/img9.jpg',
    'assets/images/img10.jpg',
    'assets/images/img11.jpg',
    'assets/images/img12.jpg',
    'assets/images/img13.jpg',
    'assets/images/img15.jpg',
    'assets/images/img16.jpg',
    'assets/images/img17.jpg',
    'assets/images/img18.jpg',
    'assets/images/img19.jpg',
    'assets/images/img20.jpg',
    'assets/images/img21.jpg',
    'assets/images/img22.jpg',
    'assets/images/img23.jpg',
    'assets/images/img24.jpg',
    'assets/images/img25.jpg',
    'assets/images/img26.jpg',
    'assets/images/img27.jpg',
    'assets/images/img28.jpg',
    'assets/images/img29.jpg',
    'assets/images/img30.jpg',
    'assets/images/img31.jpg',
    'assets/images/img33.jpg',
    'assets/images/img35.jpg',
    'assets/images/img36.jpg',
    'assets/images/img37.jpg',
    'assets/images/img38.jpg',
    'assets/images/img39.jpg',
    'assets/images/img40.jpg',
    'assets/images/img41.jpg',
    'assets/images/img42.jpg',
    'assets/images/img43.jpg',
    'assets/images/img44.jpg',
    'assets/images/img45.jpg',
    'assets/images/img46.jpg',
    'assets/images/img47.jpg',
    'assets/images/img48.jpg',
    'assets/images/img49.jpg',
    'assets/images/img50.jpg',
    'assets/images/img51.jpg',
    'assets/images/img52.jpg',
    'assets/images/img53.jpg',
    'assets/images/img54.jpg',
    'assets/images/img55.jpg',
  ];

  static const int _previewCount = 9;

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 700;

    return Container(
      color: AppTheme.creamAlt,
      padding: EdgeInsets.symmetric(
        vertical: isMobile ? 48 : 72,
        horizontal: isMobile ? 16 : 40,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(context),
          const SizedBox(height: 32),
          _buildGrid(context, isMobile),
          const SizedBox(height: 28),
          _buildVerTodasButton(context),
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
              'GALERÍA',
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
        Text('Espacios con historia', style: Theme.of(context).textTheme.headlineMedium),
        const SizedBox(height: 6),
        Container(width: 48, height: 2, color: AppTheme.gold),
        const SizedBox(height: 8),
        Text(
          '${_images.length} fotografías · mostrando $_previewCount',
          style: const TextStyle(color: AppTheme.muted, fontSize: 13),
        ),
      ],
    );
  }

  Widget _buildGrid(BuildContext context, bool isMobile) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: isMobile ? 2 : 3,
        crossAxisSpacing: isMobile ? 6 : 8,
        mainAxisSpacing: isMobile ? 6 : 8,
        childAspectRatio: 1.2,
      ),
      itemCount: _previewCount,
      itemBuilder: (context, index) {
        return GestureDetector(
          onTap: () => _openGallery(context, index),
          child: Hero(
            tag: _images[index],
            child: ClipRRect(
              borderRadius: BorderRadius.circular(6),
              child: Image.asset(
                _images[index],
                fit: BoxFit.cover,
                cacheWidth: 900,
                filterQuality: FilterQuality.high,
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildVerTodasButton(BuildContext context) {
    return Center(
      child: OutlinedButton.icon(
        onPressed: () => _openGallery(context, 0),
        icon: const Icon(Icons.photo_library_outlined, size: 18),
        label: Text('VER TODAS LAS ${_images.length} FOTOS'),
        style: OutlinedButton.styleFrom(
          foregroundColor: AppTheme.dark,
          side: const BorderSide(color: AppTheme.gold, width: 1.5),
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
          textStyle: const TextStyle(
            fontSize: 12,
            letterSpacing: 1.5,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }

  void _openGallery(BuildContext context, int initialIndex) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => _GalleryViewer(images: _images, initialIndex: initialIndex),
      ),
    );
  }
}

class _GalleryViewer extends StatefulWidget {
  final List<String> images;
  final int initialIndex;

  const _GalleryViewer({required this.images, required this.initialIndex});

  @override
  State<_GalleryViewer> createState() => _GalleryViewerState();
}

class _GalleryViewerState extends State<_GalleryViewer> {
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
            builder: (BuildContext context, int index) {
              return PhotoViewGalleryPageOptions(
                imageProvider: AssetImage(widget.images[index]),
                initialScale: PhotoViewComputedScale.contained,
                heroAttributes: PhotoViewHeroAttributes(tag: widget.images[index]),
              );
            },
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
                child: _NavButton(
                  icon: Icons.chevron_left,
                  onTap: () => _goTo(_current - 1),
                ),
              ),
            ),
          if (_current < widget.images.length - 1)
            Positioned(
              right: 16,
              top: 0,
              bottom: 0,
              child: Center(
                child: _NavButton(
                  icon: Icons.chevron_right,
                  onTap: () => _goTo(_current + 1),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

class _NavButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;
  const _NavButton({required this.icon, required this.onTap});

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
