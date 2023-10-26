import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, SafeAreaView, Button, Image } from 'react-native';
import { useEffect, useRef, useState } from 'react';
import { Camera } from 'expo-camera';
import { shareAsync } from 'expo-sharing';
import * as MediaLibrary from 'expo-media-library';


const Scan = ({ navigation }) => {
  let cameraRef = useRef();
  const [hasCameraPermission, setHasCameraPermission] = useState();
  const [hasMediaLibraryPermission, setHasMediaLibraryPermission] = useState();
  const [photo, setPhoto] = useState();
  const [showPreview, setShowPreview] = useState(false);

  useEffect(() => {
    (async () => {
      const cameraPermission = await Camera.requestCameraPermissionsAsync();
      const mediaLibraryPermission = await MediaLibrary.requestPermissionsAsync();
      setHasCameraPermission(cameraPermission.status === 'granted');
      setHasMediaLibraryPermission(mediaLibraryPermission.status === 'granted');
    })();
  }, []);

  if (hasCameraPermission === undefined) {
    return <Text>Requesting permissions...</Text>;
  } else if (!hasCameraPermission) {
    return <Text>Permission for camera not granted. Please change this in settings.</Text>;
  }

  let takePic = async () => {
    let options = {
      quality: 1,
      base64: true,
      exif: false,
    };

    let newPhoto = await cameraRef.current.takePictureAsync(options);
    setPhoto(newPhoto);
    setShowPreview(true); // Show the preview
  };

  if (photo) {
    let sharePic = () => {
      shareAsync(photo.uri).then(() => {
        setPhoto(undefined);
        setShowPreview(false);
      });
    };

    let savePhoto = () => {
      MediaLibrary.saveToLibraryAsync(photo.uri).then(() => {
        setPhoto(undefined);
        setShowPreview(false);
      });
    };

    return (
      <SafeAreaView style={styles.container}>
            {showPreview ? ( // Show the preview if showPreview is true
        <Image
            style={styles.preview}
            source={{ uri: `data:image/jpg;base64,${photo.base64}` }}
        />
        ) : ( // Show the camera view if showPreview is false
        <Camera style={styles.container} ref={cameraRef}>
            <View style={styles.buttonContainer}>
            <Button title="Take Pic" onPress={takePic} style={styles.takePicButton} />
            </View>
        </Camera>
        )}
        
        <Image
          style={styles.preview}
          source={{ uri: `data:image/jpg;base64,${photo.base64}` }}
        />
        <View style={styles.buttonContainer}>
          <Button title="Share" onPress={sharePic} style={styles.shareButton} />
          {hasMediaLibraryPermission && (
            <Button title="Save" onPress={savePhoto} style={styles.saveButton} />
          )}
          <Button title="Discard" onPress={() => setPhoto(undefined)} style={styles.discardButton} />
        </View>
        <StatusBar style="auto" />
      </SafeAreaView>
    );
  }

  return (
    <Camera style={styles.container} ref={cameraRef}>
      <View style={styles.buttonContainer}>
        <Button title="Take a clear picture of your Bill/Invoice" onPress={takePic} style={styles.takePicButton} />
      </View>
      <StatusBar style="auto" />
    </Camera>
  );
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: 'flex-start', // Align items to the left
      justifyContent: 'flex-start', // Align items to the top
      paddingHorizontal: 20, // Add some padding to the container
      paddingTop: 20, // Add some padding to the top
    },
    buttonContainer: {
      backgroundColor: '#fff',
      flexDirection: 'row',
      justifyContent: 'space-between',
      padding: 10,
      width: '100%',
    },
    button: {
      borderRadius: 5, // Make the buttons smaller by reducing the border radius
      padding: 8, // Reduce the padding to make buttons smaller
      alignItems: 'center', // Center the content inside the button
      justifyContent: 'center', // Center the content inside the button
    },
    takePicButton: {
      backgroundColor: '#000',
    },
    shareButton: {
      backgroundColor: '#00f',
    },
    saveButton: {
      backgroundColor: '#0f0',
    },
    discardButton: {
      backgroundColor: '#f00',
    },
  });
  

export default Scan;
