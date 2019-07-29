import pandas as pd



projects = pd.read_csv('result/Projects.csv')

java_projs = projects[projects['language'] == 'Java']
pd.concat([
    java_projs[java_projs['stars'] > 1000].sample(n=300),
    java_projs[(java_projs['stars'] > 100) & (java_projs['stars'] <= 1000)].sample(n=300), 
    java_projs[java_projs['stars'] <= 100].sample(n=300)
]).to_csv('temp/JavaProjectSample.csv', index=False)

py_projs = projects[projects['language'] == 'Python']
pd.concat([
    py_projs[py_projs['stars'] > 100].sample(n=500), 
    py_projs[py_projs['stars'] <= 100].sample(n=500)
]).to_csv('temp/PythonProjectSample.csv', index=False)

js_projs = projects[projects['language'] == 'JavaScript']
pd.concat([
    js_projs[js_projs['stars'] > 100].sample(n=500), 
    js_projs[js_projs['stars'] <= 100].sample(n=500)
]).to_csv('temp/JavaScriptProjectSample.csv', index=False)