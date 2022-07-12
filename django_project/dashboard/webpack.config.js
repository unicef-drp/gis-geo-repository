const path = require("path");
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin'); // require clean-webpack-plugin
// const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');

const mode = process.env.npm_lifecycle_event;
const isDev = (mode.includes('dev'));
const filename = isDev ? "[name]" : "[name].[fullhash]";
const statsFilename = isDev ? './webpack-stats.dev.json' : './webpack-stats.prod.json';
const minimized = !isDev;

let conf = {
    entry: {
        App: ['./src/App.tsx'],
        Uploader: ['./src/Uploader.tsx']
    },
    output: {
        path: path.resolve(__dirname, "./bundles/dashboard"),
        filename: filename + '.js'
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                exclude: /node_modules/,
                use: [{ loader: 'ts-loader' }],
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    // Creates `style` nodes from JS strings
                    "style-loader",
                    // Translates CSS into CommonJS
                    "css-loader",
                    // Compiles Sass to CSS
                    "sass-loader",
                ],
            },
            {
                test: /\.css$/i,
                use: [
                    // Translates CSS into CommonJS
                    "css-loader",
                ],
            },
        ],
    },
    optimization: {
        minimize: minimized
    },
    plugins: [
        new CleanWebpackPlugin(),
        new BundleTracker({ filename: statsFilename }),
        new MiniCssExtractPlugin({
            filename: filename + '.css',
            chunkFilename: filename + '.css',
        }),
    ],
    resolve: {
        modules: ['node_modules'],
        extensions: [".ts", ".tsx", ".js", ".css", ".scss"]
    },
    watchOptions: {
        ignored: ['node_modules', './**/*.py'],
        aggregateTimeout: 300,
        poll: 1000
    }
};
if (isDev) {
    conf['output'] = {
        path: path.resolve(__dirname, "./bundles/dashboard"),
        filename: filename + '.js',
    }
    conf['devServer'] = {
        hot: true,
        port: 9000
    }
    // conf['plugins'].push(
    //     isDev && new ReactRefreshWebpackPlugin()
    // )
}
module.exports = conf;
