// Automatic FlutterFlow imports
import '/backend/backend.dart';
import '/backend/schema/structs/index.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'dart:developer';

Future queryDocumentNames() async {
  // Get a list of places collection "name" fields, for each place with a Document ID in the App State
// Assuming the App State has a list of Document IDs called "documentIds"

  List<String> placeNames = [];

  for (String id in FFAppState().queryDocumentIDs) {
    DocumentSnapshot snapshot =
        await FirebaseFirestore.instance.collection('places').doc(id).get();
    if (snapshot.exists) {
      dynamic data = snapshot.data();
      placeNames.add(data['name']);
    }
  }

  FFAppState().queryDocumentNames = placeNames;
}
