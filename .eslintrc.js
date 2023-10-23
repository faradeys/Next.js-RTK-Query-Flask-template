module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'next',
    'next/core-web-vitals',
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  plugins: ['prettier', 'unused-imports', 'react', 'prefer-arrow', '@typescript-eslint'],
  parserOptions: {
    ecmaFeatures: {
      legacyDecorators: true,
      jsx: true,
    },
    tsconfigRootDir: __dirname,
    project: './tsconfig.json',
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  rules: {
    'no-shadow': 'off',
    'prettier/prettier': 'error',
    'no-console': 'error',
    '@typescript-eslint/array-type': [
      'error',
      {
        default: 'array-simple',
      },
    ],
    '@typescript-eslint/consistent-type-definitions': 'error',
    '@typescript-eslint/explicit-member-accessibility': [
      'off',
      {
        accessibility: 'explicit',
      },
    ],
    '@typescript-eslint/member-delimiter-style': [
      'error',
      {
        multiline: {
          delimiter: 'none',
          requireLast: true,
        },
        singleline: {
          delimiter: 'semi',
          requireLast: false,
        },
      },
    ],
    '@typescript-eslint/naming-convention': [
      'error',
      {
        selector: 'default',
        format: ['camelCase', 'PascalCase'],
        filter: {
          regex: '^_+$',
          match: false,
        },
      },
      {
        selector: 'variable',
        format: ['camelCase', 'UPPER_CASE', 'PascalCase'],
      },
      {
        selector: 'parameter',
        format: ['camelCase', 'PascalCase'],
        leadingUnderscore: 'allow',
        filter: {
          regex: '^_+$',
          match: false,
        },
      },
      {
        selector: 'property',
        format: null,
      },
      {
        selector: 'typeLike',
        format: ['PascalCase'],
      },
      {
        selector: 'enumMember',
        format: ['PascalCase', 'UPPER_CASE', 'camelCase'],
      },
    ],
    '@typescript-eslint/no-empty-interface': 'off',
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-inferrable-types': [
      'error',
      {
        ignoreParameters: true,
        ignoreProperties: true,
      },
    ],
    '@typescript-eslint/no-require-imports': 'off',
    '@typescript-eslint/no-this-alias': 'error',
    'arrow-parens': ['error', 'always'],
    'comma-dangle': ['error', 'always-multiline'],
    eqeqeq: ['error', 'smart'],
    'id-blacklist': ['warn', 'any', 'Number', 'String', 'string', 'Boolean', 'boolean', 'Undefined', 'undefined'],
    'id-match': 'error',
    'import/no-extraneous-dependencies': 'off',
    'import/no-internal-modules': 'off',
    'import/order': 'off',
    'object-shorthand': ['error', 'always'],
    'prefer-arrow/prefer-arrow-functions': 'error',
    'prefer-object-spread': 'off',
    'react/jsx-boolean-value': 'error',
    'spaced-comment': [
      'error',
      'always',
      {
        markers: ['/'],
      },
    ],
    'array-bracket-spacing': ['error', 'never'],
    '@typescript-eslint/ban-ts-comment': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-shadow': 'error',
    'react/prop-types': 'off',
    'react/display-name': 'off',
    'no-prototype-builtins': 'off',
    'jsx-quotes': ['error', 'prefer-single'],
    'react/jsx-no-bind': ['error', { allowArrowFunctions: true }],
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'error',
    'react/function-component-definition': ['error', { namedComponents: 'arrow-function' }],
    '@typescript-eslint/no-explicit-any': 'off',
  },
  globals: {
    React: true,
  },
}
