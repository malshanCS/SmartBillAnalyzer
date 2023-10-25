import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const Expenses = ({ navigation }) => {
    return (
        <View style={styles.container}>
            <Text>Expenses</Text>
            <Button
                title="Click Here"
                onPress={() => navigation.navigate('Button Cicked!')}
            />
        </View>
    );
}

export default Expenses;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor:'#000000'
    }
});

