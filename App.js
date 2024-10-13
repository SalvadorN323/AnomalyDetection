import React, {useEffect, useState} from 'react';
import { SafeAreaView, Text, StyleSheet, View, Image, ActivityIndicator, FlatList } from 'react-native';
import D from './data.json';
import { ScrollView } from 'react-native-web';

const App = () => {
    return (
        <View style = {{flex: 1}}>
         q   <ScrollView>
                {D.map((item) => {
                    return (
                        <View
                            style = {{
                                width: '100%',
                                height: 50,
                                flexDirection: 'row',
                                justifyContent: 'space-between',
                            }}>
                            <Text>{item.name}</Text>
                        </View>
                    );
                })}
            </ScrollView>
        </View>                   

    );
};
    // const [data, setData] = useState(null);
    // const [loading, setLoading] = useState(true);

    // useEffect(() => {
    // const fetchData = async () => {
    //     try {
    //         const response = await fetch('http://127.0.0.1:5000/output1'); // Adjust the URL as needed
    //         const json = await response.json();
    //         setData(json);
    //     } catch (error) {
    //         console.error(error);
    //     } finally {
    //         setLoading(false);
    //     }
    // console.log(data);
    // };

//     fetchData();
//   }, []);

//   if (loading) {
//     return <ActivityIndicator size="large" color="#0000ff" />;
//   }


//   return (

//     //create a simple user message with company Logo
//     <View style={styles.container}>

//         {/* <Text style={styles.text}>Hello, World!</Text>
//         <Image 
//         source = {require('./assets/morning_star_logo_sticky-removebg-preview.png')}
//         style={styles.Image}
//         />  */}
//         <Text></Text>
//     </View>

    

//   );
// };

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: '#F5FCFF',
//   },
//   text: {
//     fontSize: 24,
//     fontWeight: 'bold',
//   },
//   image: {
//     width: 200,
//     height: 200,
//   },
// });

export default App;

