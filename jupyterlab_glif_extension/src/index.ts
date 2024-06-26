import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
    IEditorLanguageRegistry
} from '@jupyterlab/codemirror';


// import { sql } from '@codemirror/lang-sql';
import {GLIFCell} from 'codemirror-lang-glif';


/**
 * Initialization data for the jupyter_glif extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
    id: 'jupyter_glif:plugin',
    description: 'A JupyterLab extension for GLIF (for now, just syntax highlighting)',
    autoStart: true,
    requires: [IEditorLanguageRegistry],
    activate: (app: JupyterFrontEnd, registry: IEditorLanguageRegistry) => {
        console.log('JupyterLab extension jupyter_glif is activated!');

        // register the GLIF language
        registry.addLanguage({
            name: 'glif',
            mime: 'text/glif',
            support: GLIFCell()
        });

        // Add CSS
        const head = document.head || document.getElementsByTagName('head')[0];
        const style = document.createElement('style');
        style.textContent = ".glif-stderr { padding-left: 0.5em; background-color: #ffcccc; border-left: 0.5em solid; border-color: #000000; } .glif-stdout { padding-left: 0.5em; border-left: 0.5em solid; border-color: a0a0a0; }";
        head.appendChild(style);

        console.log('JupyterLab extension jupyter_glif is activated DONE!');
    }
};

export default plugin;
