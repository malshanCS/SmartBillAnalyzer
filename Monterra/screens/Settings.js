import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const Settings = ({ navigation }) => {
    return (
        <View style={styles.container}>
            <Text>Settings</Text>
            <Button
                title="Click Here"
                onPress={() => navigation.navigate('Button CLicked!')}
            />
        </View>
    );
}

export default Settings;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor:'#8fcbbc'
    }
});

