import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const Add = ({ navigation }) => {
    return (
        <View style={styles.container}>
            <Text>Add</Text>
            <Button
                title="Click Here"
                onPress={() => navigation.navigate('Button CLicked!')}
            />
        </View>
    );
}

export default Add;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor:'#8fcbbc'
    }
});

