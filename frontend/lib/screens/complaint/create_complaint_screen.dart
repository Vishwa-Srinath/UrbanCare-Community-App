import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart' as osm;
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:image_picker/image_picker.dart';
import 'package:latlong2/latlong.dart' as latlng;
import 'package:urbancare_frontend/models/location.dart';
import 'package:urbancare_frontend/repositories/complaint_repository.dart';
import 'package:urbancare_frontend/widgets/primary_button.dart';
import 'package:urbancare_frontend/widget/text_input.dart';

class CreateComplaintScreen extends StatefulWidget {
  const CreateComplaintScreen({
    super.key,
    required this.complaintRepository,
  });

  final ComplaintRepository complaintRepository;

  @override
  State<CreateComplaintScreen> createState() => _CreateComplaintScreenState();
}

class _CreateComplaintScreenState extends State<CreateComplaintScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();

  final _picker = ImagePicker();

  bool _loadingLocation = true;
  bool _submitting = false;
  bool _manualLocationMode = false;
  AppLocation? _location;
  AppLocation? _selectedLocation;
  XFile? _pickedImage;
  String _issueTYpe = 'road_damage';

  static const _issueItem = <String, String>{
    'road_damage': '🚧 Road Damage',
    'streetlight': '💡 Street Light',
    'garbage': '🗑️ Garbage',
    'water': '🌊 Water / Flooding',
    'other': '📌 Other',
  };

  @override
  void initState() {
    super.initState();
    _loadLocation();
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  Future<void> _loadLocation() async {
    setState(() => _loadingLocation = true);
    try {
      final location = await widget.complaintRepository.getCurrentLocation();
      if(!mounted) return;
      setState(() {
        _location = location;
        if(_manualLocationMode) {
          _selectedLocation ??= location;
        } else{
          _selectedLocation = location;
        }
      });
    }catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString())),
      );
    } finally {
      if(mounted) {
        setState(() => _loadingLocation = false);
      }
    }
  }

  String _formatCoordinates(AppLocation location) {
    return '${location.latitude.toStringAsFixed(5)}, '
        '${location.longitude.toStringAsFixed(5)}';
  }

  void _toggleManualLocationMode(bool enabled) {
    setState(() {
      _manualLocationMode = enabled;

      // Manual mode off means user wants to use current GPS location directly.
      if (!enabled && _location != null) {
        _selectedLocation = _location;
      }
    });
  }

  void _selectLocation(double latitude, double longitude) {
    if (!_manualLocationMode) {
      return;
    } 

    setState(() {
      _selectedLocation = AppLocation(
        latitude: latitude,
        longitude: longitude,
        address: _location?.address ?? 'Selected from map',
        city: _location?.city,
        district: _location?.district,
      );
    });
  }

  void _selectLocationOnGoogleMap(LatLng target) {
    _selectLocation(target.latitude, target.longitude);
  }

  void _selectLocationOnOsmMap(latlng.LatLng target){
    _selectLocation(target.latitude,target.longitude);
  }

  Set<Marker> _buildLocationMarkers() {
    final markers = <Marker>{};

    if (_location != null) {
      markers.add(
        Marker(
          markerId: const MarkerId('current_location'),
          position: LatLng(_location!.latitude, _location!.longitude),
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueAzure),
          infoWindow: const InfoWindow(title: 'Current location'),
        ),
      );
    }

    if (_selectedLocation != null) {
      markers.add(
        Marker(
          markerId: const MarkerId('selected_location'),
          position: LatLng(
            _selectedLocation!.latitude,
            _selectedLocation!.longitude,
          ),
          infoWindow: const InfoWindow(title: 'Selected report location'),
        ),
      );
    }

    return markers;
  }

  List<osm.Marker> _buildOsmLocationMarkers() {
    final markers = <osm.Marker>[];

    if(_location != null) {
      markers.add(
        osm.Marker(
          point: latlng.LatLng(_location!.latitude, _location!.longitude),
          width: 42,
          height: 42,
          child: const Icon(
            Icons.my_location,
            color: Color(0xFF60A5FA),
            size: 30,
          ),
        ),
      );
    }

    if (_selectedLocation != null) {
      markers.add(
        osm.Marker(
          point: latlng.LatLng(
            _selectedLocation!.latitude,
            _selectedLocation!.longitude,
          ),
          width: 38,
          height: 38,
          child: const Icon(
            Icons.location_on,
            color: Color(0xFFF59E0B),
            size: 32,
          ),
        ),
      );
    }

    return markers;
  }

}