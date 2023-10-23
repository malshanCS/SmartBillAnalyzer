import React from 'react';
import { View, Text, Button, StyleSheet, ImageBackground, TextInput} from 'react-native';


const Scan = ({ navigation }) => {
    return (
        <View style={styles.container}>
            <Text>Scan</Text>
            <Button
                title="Click Here"
                onPress={() => navigation.navigate('Button CLicked!')}
            />
        </View>
    );
}

export default Scan;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor:'#8fcbbc'
    }
});

