import 'package:flutter/material.dart';
import 'package:urbancare_frontend/models/complaint.dart';
import 'package:urbancare_frontend/repositories/complaint_repository.dart';
import 'package:urbancare_frontend/widgets/primary_button.dart';

class ComplaintDetailScreen extends StatefulWidget{
  const ComplaintDetailScreen({
    super.key,
    required this.complaint,
    required this.complaintRepository,
  });

  final ComplaintModel complaint;
  final ComplaintRepository complaintRepository;

  @override
  State<ComplaintDetailScreen> createState() => _ComplaintDetailScreenState();
}

class _ComplaintDetailScreenState extends State<ComplaintDetailScreen>{
  late ComplaintModel _complaint;
  bool _loading = true;
  Bool _verifying = false;

  @override
  void initState() {
    super.initState();
    _complaint = widget.complaint;
    _loadLatest();
  }

  Future<void> _loadLatest() async {
    try{
      final fresh=
        await widget.complaintRepository.getComplaintById(_complaint.complaintId);

      if(!mounted) return;
      setState((){
        _complaint = ComplaintModel(
          complaintId: fresh.complaintId,
          issueType: fresh.issueType.isEmpty ? _complaint.issueType : fresh.issueType,
          description: fresh.description.isEmpty
              ? _complaint.description
              : fresh.description,
          status: fresh.status,
          citizenId: fresh.citizenId ?? _complaint.citizenId,
          locationId: fresh.locationId ?? _complaint.locationId,
          location: _complaint.location ?? fresh.location,
          distanceMeters: _complaint.distanceMeters ?? fresh.distanceMeters,
          primaryImageUrl: fresh.primaryImageUrl ?? _complaint.primaryImageUrl,
        );
      });  
    }catch (_) {

    }finally {
      if(mounted) {
        setState(()=>_loading = false);
      }
    }
  }

  Future<void> _verify({
    required bool isFixed,
    required String successMessage,
  }) async {
    if (_verifying) {
      return;
    }

    setState(()=> _verifying = true);
    try {
      final updated = await widget.complaintRepository.verifyComplaint(
        complaintId: _complaint.complaintId,
        isFixed: isFixed,
      );

      if(!mounted) return;
      setState((){
        _complaint = ComplaintModel(
          complaintId: updated.complaintId,
          issueType:
              updated.issueType.isEmpty ? _complaint.issueType : updated.issueType,
          description:
              updated.description.isEmpty ? _complaint.description : updated.description,
          status: updated.status,
          citizenId: updated.citizenId ?? _complaint.citizenId,
          locationId: updated.locationId ?? _complaint.locationId,
          location: _complaint.location,
          distanceMeters: _complaint.distanceMeters,
          primaryImageUrl: _complaint.primaryImageUrl,
        );
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(successMessage)),
      );   
    }catch(e){
      if(!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString())),
      );  
    }finally {
      if(mounted){
        setState(()=> _verifying = false);
      }
    }
  }
}