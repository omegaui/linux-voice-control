
import 'package:bitsdojo_window/bitsdojo_window.dart';
import 'package:flutter/material.dart';
import 'package:lvc_gui_flutter/themex.dart';
import 'package:lvc_gui_flutter/ui/app_indicator.dart';
import 'package:lvc_gui_flutter/ui/app_indicator_text.dart';
import 'package:lvc_gui_flutter/ui/status_indicator.dart';

class HomeScreen extends StatefulWidget{
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => HomeScreenState();
}

class HomeScreenState extends State<HomeScreen> {

  void rebuild() => setState(() {});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: ThemeX.backgroundColor,
      width: MediaQuery.of(context).size.width,
      height: MediaQuery.of(context).size.height,
      child: Stack(
        children: [
          Align(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                AppIndicator(),
                SizedBox(height: 10),
                AppIndicatorText(),
                SizedBox(height: 4),
                StatusIndicator(),
              ],
            ),
          ),
          Align(
            alignment: Alignment.center,
            child: MoveWindow(
              child: SizedBox(
                width: MediaQuery.of(context).size.width,
                height: MediaQuery.of(context).size.height,
              ),
            ),
          ),
        ],
      ),
    );
  }
}


