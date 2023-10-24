import React, { useState, useEffect, useRef } from 'react';
import { View, Text, Button, StyleSheet, TouchableOpacity, Image } from 'react-native';
import { Camera } from 'expo-camera';

const Scan = ({ navigation }) => {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraType, setCameraType] = useState(Camera.Constants.Type.back);
  const cameraRef = useRef(null);
  const [imageData, setImageData] = useState('');

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (cameraRef.current) {
      const { uri } = await cameraRef.current.takePictureAsync(); // Take a picture and get the URI
      setImageData(uri);
    }
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={{ flex: 1 }}>
      {imageData === '' ? (
        <View style={{ flex: 1 }}>
          <Camera
            ref={cameraRef}
            style={StyleSheet.absoluteFill}
            type={cameraType}
          />
          <TouchableOpacity
            style={{
              width: 60,
              height: 60,
              borderRadius: 30,
              backgroundColor: '#FF0037',
              position: 'absolute',
              bottom: 50,
              alignSelf: 'center',
            }}
            onPress={takePicture} // Call takePicture when you want to capture an image
          ></TouchableOpacity>
        </View>
      ) : (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <Image source={{ uri: imageData }} style={{ width: '90%', height: 200 }} />
          <TouchableOpacity
            style={{
              width: '90%',
              height: 50,
              borderWidth: 1,
              alignSelf: 'center',
              borderRadius: 10,
              justifyContent: 'center',
              alignItems: 'center',
            }}
            onPress={() => setImageData('')}
          >
            <Text>Take Another Photo</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

export default Scan;
