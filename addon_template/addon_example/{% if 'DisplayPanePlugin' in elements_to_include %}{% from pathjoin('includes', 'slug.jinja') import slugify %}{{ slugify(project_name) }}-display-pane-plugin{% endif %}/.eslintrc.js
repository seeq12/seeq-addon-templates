module.exports = {
    "env": {
        "commonjs": true,
        "node": true
    },
    "extends": [],
    "settings": {
        "react": {
            "version": "detect"
        }
    },
    "parserOptions": {
        "ecmaFeatures": {
            "jsx": true
        },
        "ecmaVersion": 11,
        "sourceType": "script"
    },
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
        'ecmaVersion': 2019
    },
    "rules": {
        "semi": ["error", "always"]
    },
    "overrides": [
        {
            "files": ["src/**"],
            "env": {
                "browser": true
            },
            "parserOptions": {
                "ecmaFeatures": {
                    "jsx": true
                },
                "ecmaVersion": 11,
                "sourceType": "module"
            },
        }, 
        {
            "files": ["**/*.test.{ts,tsx,js,jsx}"],
            "env": {
                "jest": true,
                "browser": true
            },
            "parserOptions": {
                "ecmaFeatures": {
                    "jsx": true
                },
                "ecmaVersion": 11,
                "sourceType": "module"
            },
        }
    ],
    "plugins": [
        "react",
        "@typescript-eslint"
    ]
};
