import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const Reports = ({ navigation }) => {
    return (
        <View style={styles.container}>
            <Text>Reports</Text>
            <Button
                title="Click here"
                onPress={() => navigation.navigate('Button CLicked!')}
            />
        </View>
    );
}

export default Reports;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor:'#8fcbbc'
    }
});

