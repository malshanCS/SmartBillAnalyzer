import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';

import React from 'react';
import  Expenses from '../screens/Expenses';
import  Reports  from '../screens/Reports';
import  Add  from '../screens/Add';
import  Settings  from '../screens/Settings';
import  Scan  from '../screens/Scan';


const Tab = createBottomTabNavigator();

const CustomTabBarButton = ({children, onPress}) => (
    <TouchableOpacity
        style={{
            top: -30,
            justifyContent: 'center',
            alignItems: 'center',
            ...styles.shadow
        }}
        onPress={onPress}
    >
        <View style= {{
            width: 70,
            height: 70,
            borderRadius: 35,
            backgroundColor: '#e32f45'
        }}>
          {children}
        </View>
    </TouchableOpacity>
);  

const Tabs = () => {
  return (
    <Tab.Navigator
        screenOptions={{
            tabBarShowLabel: false,
            tabBarStyle: {
                position: 'absolute',
                bottom: 25,
                left: 20,
                right: 20,
                elevation: 0,
                backgroundColor: '#ffffff',
                borderRadius: 15,
                height: 90,
                ...styles.shadow
            }
        }} 
    >
        <Tab.Screen name="Expenses" component={Expenses} 
        options = {{
            tabBarIcon: ({focused}) => (
                <View style={{alignItems: 'center', justifyContent: 'center', top: 10}}>
                    <Image 
                        source={require('../assets/expenses.png')}
                        resizeMode='contain'
                        style={{
                            width: 25,
                            height: 25,
                            tintColor: focused ? '#e32f45' : '#748c94'
                        }}
                    />
                    <Text style={{color: focused ? '#e32f45' : '#748c94', fontSize: 10}}>Expenses</Text>
                </View>
            )
        }}
        />
        <Tab.Screen name="Reports" component={Reports} 
        options = {{
          tabBarIcon: ({focused}) => (
              <View style={{alignItems: 'center', justifyContent: 'center', top: 10}}>
                  <Image 
                      source={require('../assets/reports.png')}
                      resizeMode='contain'
                      style={{
                          width: 25,
                          height: 25,
                          tintColor: focused ? '#e32f45' : '#748c94'
                      }}
                  />
                  <Text style={{color: focused ? '#e32f45' : '#748c94', fontSize: 10}}>Reports</Text>
              </View>
          )
      }}
        />
        <Tab.Screen name="Scan" component={Scan} 
        options = {{
          tabBarIcon: ({focused}) => (
              <Image 
                  source={require('../assets/scan.png')}
                  resizeMode='contain'
                  style={{
                      width: 25,
                      height: 25,
                      tintColor: '#fff'
                  }}
              />
          ),
          tabBarButton: (props) => (
              <CustomTabBarButton {...props} />
          )
        }}
        />
        <Tab.Screen name="Add" component={Add} 
        options = {{
          tabBarIcon: ({focused}) => (
              <View style={{alignItems: 'center', justifyContent: 'center', top: 10}}>
                  <Image 
                      source={require('../assets/add.png')}
                      resizeMode='contain'
                      style={{
                          width: 25,
                          height: 25,
                          tintColor: focused ? '#e32f45' : '#748c94'
                      }}
                  />
                  <Text style={{color: focused ? '#e32f45' : '#748c94', fontSize: 10}}>Add</Text>
              </View>
          )
      }}
        />
        <Tab.Screen name="Settings" component={Settings} 
        options = {{
          tabBarIcon: ({focused}) => (
              <View style={{alignItems: 'center', justifyContent: 'center', top: 10}}>
                  <Image 
                      source={require('../assets/settings.png')}
                      resizeMode='contain'
                      style={{
                          width: 25,
                          height: 25,
                          tintColor: focused ? '#e32f45' : '#748c94'
                      }}
                  />
                  <Text style={{color: focused ? '#e32f45' : '#748c94', fontSize: 10}}>Settings</Text>
              </View>
          )
      }}
        />
    </Tab.Navigator>
  );
}

const styles = {
    shadow: {
        shadowColor: '#7F5DF0',
        shadowOffset: {
            width: 0,
            height: 10,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.5,
        elevation: 5
    }
}

export default Tabs;