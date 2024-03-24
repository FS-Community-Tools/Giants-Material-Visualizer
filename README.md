# Giants Material Visualizer

<p align="left">
  <a href="https://github.com/StjerneIdioten/I3D-Blender-Addon/releases/latest/download/i3d_exporter.zip">Download Newest Release</a> •
  <a href="https://github.com/StjerneIdioten/I3D-Blender-Addon/releases">All Releases</a> •
</p>

## Description

A Blender addon for visualizing materials in the I3D format used by the Giants Engine. The addon is designed to be a tool for modders to easily visualize and tweak materials in Blender, and then export them to the I3D format.

## Installation

Installation of the addon is done by downloading the latest release from the [releases page]() and installing it in Blender. The installation process is as follows:

1. Download the latest release from the [releases page]()
2. Open Blender
3. Go to `Edit` -> `Preferences` -> `Add-ons` -> `Install...`
4. Select the downloaded zip file and click `Install Add-on`
5. Enable the addon by checking the box next to `Giants Material Visualizer` in the list of addons
6. Click `Save Preferences` to save the changes
7. The addon is now installed and ready to use

## Usage
Addon does not break the material setting for the export, so even visualized materials can be exported without any issues.

The addon is designed to be as user-friendly as possible, and the usage is as follows:

1. Go to the `Material` tab in the `Properties` panel
2. Select the material you want to visualize
3. Click the `Enable Visualization` button in the `Material Visualizer` panel

    ![](img/img_1.png)

#### Shader Parameters

<img src="/img/img_2.png" alt="Shader Parameters" height="512"/>

For now, all the features support just [Community I3D Exporter](https://github.com/StjerneIdioten/I3D-Blender-Addon)

#### All the features works just when the shader is selected and shader type contains `colorMask`.

- **Real Time Update** - Updates the shader values _**in real time**_ that will be exported (Visualizer Parameters -> Shader Parameters)
- **Get** - Updates the shader values that will be exported (Visualizer Parameters -> Shader Parameters)
- **Set** - Updates the visualizer values from the shader (Shader Parameters -> Visualizer Parameters)

## Known Issues
When the shader is first time imported, user needs to click twice to enable Visualization (this happens just in case when shader was not already imported in the scene). 
It is caused by handler that is triggered before the material is constructed.

## What's Next
- Add support for official Giants I3D Exporter
- Add UDIM picker

## Help

If you need help with the addon in any way, the following channels are available:

* [Issue Tracker](https://github.com/FS-Community-Tools/Giants-Material-Visualizer/issues): If you come across any bugs, please post them here.
* [AgroSketch Discord](https://discord.gg/Qb6hq5z): There is an official support channel available for the exporter
* [VertexDezign Discord](https://discord.com/invite/vertexdezign): There is an official support channel available for the exporter